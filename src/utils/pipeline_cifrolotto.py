import subprocess
import os

def execute_command(command, working_dir=None):
    """
    Esegue un comando shell in una directory specifica e restituisce l'output.
    """
    try:
        result = subprocess.run(command, shell=True, cwd=working_dir, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando: {e}")
        print("Uscita standard:\n", e.stdout)
        print("Errore standard:\n", e.stderr)
        return None

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))  # Root del progetto
    scripts_dir = os.path.join(project_root, "scripts")  # Path relativo alla cartella scripts
    config_path = os.path.join(project_root, "config.ini")  # Path del file config.ini

    # Percorsi completi per i file Python
    categorizer_script = os.path.join(project_root, "src/utils/cifrolotto_categorizer.py")
    analysis_script = os.path.join(project_root, "src/utils/cifrolotto.py")

    # Passo 1: Esegui lo scraping
    print("Esecuzione dello scraping...")
    print(f"[DEBUG] Directory di lavoro: {scripts_dir}")
    scraping_output = execute_command("bash get_all.sh", working_dir=scripts_dir)
    if scraping_output is None:
        print("Errore durante lo scraping. Interruzione della pipeline.")
        return

    print("Scraping completato. Risultati acquisiti.")

    # Passo 2: Esegui il categorizzatore
    print("Avvio del categorizzatore...")
    categorizer_command = f"python {categorizer_script}"
    categorizer_output = execute_command(categorizer_command, working_dir=project_root)
    if categorizer_output is None:
        print("Errore durante la categorizzazione. Interruzione della pipeline.")
        return
    
    print("Categorizzazione completata.")
    
    # Passo 3: Esegui le analisi statistiche
    print("Avvio delle analisi statistiche...")
    analysis_command = f"python {analysis_script}"
    analysis_output = execute_command(analysis_command, working_dir=project_root)
    if analysis_output is None:
        print("Errore durante l'analisi statistica. Interruzione della pipeline.")
        return
    
    print("Analisi statistiche completate.")
    print("Pipeline completata con successo!")

if __name__ == "__main__":
    main()
