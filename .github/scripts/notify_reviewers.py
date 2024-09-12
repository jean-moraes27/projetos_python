import os
import requests

# Obtenha as variáveis de ambiente
github_token = os.getenv("GITHUB_TOKEN")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("GITHUB_EVENT_PULL_REQUEST_NUMBER")

# Cabeçalhos da requisição para a API do GitHub
headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

# Endpoint para buscar informações sobre a PR
pr_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}"

response = requests.get(pr_url, headers=headers)
pr_data = response.json()

# Pegar os usuários responsáveis pelo review
requested_reviewers = pr_data.get("requested_reviewers", [])

# Verifica se há revisores atribuídos
if requested_reviewers:
    reviewers_names = [user['login'] for user in requested_reviewers]
    reviewers_list = ", ".join(reviewers_names)

    # Mensagem a ser enviada para o Slack
    message = {
        "text": f"🚨 Atenção: Revisores solicitados para a PR #{pr_number} no repositório {repo_name}: {reviewers_list}"
    }

    # Envia notificação para o Slack
    slack_response = requests.post(slack_webhook_url, json=message)

    if slack_response.status_code != 200:
        raise ValueError(f"Erro ao enviar notificação ao Slack: {slack_response.status_code}, {slack_response.text}")
else:
    print("Nenhum revisor atribuído a essa PR.")
