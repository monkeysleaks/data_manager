import os
from cloudflare import Cloudflare
from dotenv import load_dotenv
load_dotenv()

client = Cloudflare(
    api_email= os.getenv("CLOUDFLARE_EMAIL"),  # This is the default and can be omitted
    api_key=os.getenv("CLOUDFLARE__API_KEY"),  # This is the default and can be omitted
)
def obtener_id_deploment():
    page = client.pages.projects.deployments.list(
        project_name=os.getenv("CF_PROJECT_NAME"),
        account_id=os.getenv("CF_ACCOUNT_ID"),
    )
    page = page.result[0]
    # print(page.id)
    return page.id

def retry_deployment(deploy_id):
    deployment = client.pages.projects.deployments.retry(
        deployment_id=deploy_id,
        account_id=os.getenv("CF_ACCOUNT_ID"),
        project_name=os.getenv("CF_PROJECT_NAME"),
        body={},
    )

    # print(deployment.id)
def main():
   

    client = Cloudflare(
        api_email=os.environ.get("CLOUDFLARE_EMAIL"),  # This is the default and can be omitted
        api_key=os.environ.get("CLOUDFLARE_API_KEY"),  # This is the default and can be omitted
    )
    deploy_id =obtener_id_deploment()
    retry_deployment(deploy_id)
    print("ejecucion completa") 

if __name__ == "__main__":
     main()
    