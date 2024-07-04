const { Octokit } = require("@octokit/rest");
const axios = require("axios");

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
const slaHours = parseInt(process.env.SLA_HOURS, 10) || 48;
const slackWebhookUrl = process.env.SLACK_WEBHOOK_URL;
const repoOwner = process.env.GITHUB_REPOSITORY.split('/')[0];
const repoName = process.env.GITHUB_REPOSITORY.split('/')[1];

async function checkPrSla() {
  const pulls = await octokit.pulls.list({
    owner: repoOwner,
    repo: repoName,
    state: 'open'
  });

  const now = new Date();
  const alerts = [];
  for (const pull of pulls.data) {
    const createdDate = new Date(pull.created_at);
    const diffTime = Math.abs(now - createdDate);
    const diffHours = Math.ceil(diffTime / (1000 * 60 * 60));

    if (diffHours > slaHours) {
      alerts.push(`:warning: PR #${pull.number}: *${pull.title}* não foi revisado dentro do prazo de SLA de ${slaHours} horas. <${pull.html_url}|Veja o PR>`);
    }
  }

  if (alerts.length > 0) {
    const message = {
      text: `:bell: Alertas de SLA para Revisão de Pull Requests:\n\n${alerts.join('\n')}`
    };

    await axios.post(slackWebhookUrl, message);
  }
}

checkPrSla().catch(err => console.error(err));
