from bot.db.repositories.repository import Repo, RepoConfig
from bot.db.repositories.sa_repository import SARepo
from bot.db.db_sa_settings import sa_repo_config


def get_repo(repo_type: str, repo_config: RepoConfig | None = None) -> Repo:
    match repo_type:
        case "sa":
            return SARepo(repo_config or sa_repo_config)

    raise ValueError(f"No such repo type: {repo_type}. Available types: 'sa'.")
