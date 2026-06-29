from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../chave/dsalab-c2eb2fcd348c.json"

project_id = "dsalab"
dataset_id = "dsastaging"

csv_directory = "dados"  

client = bigquery.Client(project=project_id)

def dsa_cria_dataset(dataset_id):

    dataset_ref = f"{project_id}.{dataset_id}"

    dataset = bigquery.Dataset(dataset_ref)

    dataset.location = "US"  

    try:
        client.get_dataset(dataset_ref)  
        print(f"Dataset '{dataset_id}' já existe.")
    except Exception:
        dataset = client.create_dataset(dataset)
        print(f"Dataset '{dataset_id}' criado com sucesso.")

def dsa_carrega_bigquery(table_name, csv_file_path):

    table_id = f"{project_id}.{dataset_id}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  
        autodetect=True       
    )
    
    with open(csv_file_path, "rb") as file:
        load_job = client.load_table_from_file(file, table_id, job_config=job_config)
        load_job.result() 

    print(f"Tabela {table_name} criada com sucesso.")

dsa_cria_dataset(dataset_id)

csv_files = {
    "stg_clientes": os.path.join(csv_directory, "stg_clientes.csv"),
    "stg_data": os.path.join(csv_directory, "stg_data.csv"),
    "stg_localidades": os.path.join(csv_directory, "stg_localidades.csv"),
    "stg_produtos": os.path.join(csv_directory, "stg_produtos.csv"),
    "stg_vendas": os.path.join(csv_directory, "stg_vendas.csv")
}

for table_name, csv_file_path in csv_files.items():
    dsa_carrega_bigquery(table_name, csv_file_path)








