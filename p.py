import re
import subprocess

###################################################################################################
## REDUZIR TAMANHO: ffmpeg -i input_video.mp4 -vf scale=1280:720 -c:a copy output_video_720p.mp4 ##
###################################################################################################

###############################################################################
## Abrir iFrame do vídeo em nova aba, Inspecionar e Buscar por "playerConfig" ##
###############################################################################

#############################################
## Inspecionar e Buscar por "playerConfig" ##
#############################################

def extract_video_url(config_text):
    #######################################################
    ## Regex para capturar URLs HLS (m3u8) e DASH (json) ##
    #######################################################
    hls_url_pattern = r'"url":"(https://[^"]+\.m3u8[^"]*)"'
    
    #######################################
    ## Buscar as URLs no texto do código ##
    #######################################
    hls_url_match = re.search(hls_url_pattern, config_text)
    
    ###################################################
    ## Selecionar HLS se disponível, senão usar DASH ##
    ###################################################
    if hls_url_match:
        video_url = hls_url_match.group(1).replace("\\u0026", "&")
    else:
        print("Nenhuma URL de vídeo encontrada no trecho de código.")
        return None
    
    return video_url

def extract_title(config_text):
    ##############################################################
    ## Regex para capturar o conteúdo da tag <title> no HTML ##
    ##############################################################
    title_pattern = r"<title>(.*?)</title>"
    title_match = re.search(title_pattern, config_text, re.IGNORECASE)
    
    ##################################################
    ## Retorna o título ou um nome padrão se faltar ##
    ##################################################
    return title_match.group(1) if title_match else "video"

def download_video(video_url, output_name):
    try:
        #############################################
        ## Executa o FFmpeg para baixar o vídeo    ##
        #############################################
        command = ["ffmpeg", "-i", video_url, "-c", "copy", output_name]
        subprocess.run(command, check=True)
        print(f"Download concluído: {output_name}")
    except subprocess.CalledProcessError:
        print("Erro ao executar o FFmpeg.")

#####################################
## Ler o arquivo media.txt no local ##
#####################################

try:
    with open("media.txt", 'r', encoding='utf-8') as file:
        config_text = file.read()
    
    ##############################################
    ## Extraindo título e definindo o nome final##
    ##############################################
    title = extract_title(config_text)
    output_name = f"{title}.mp4"

    ################################################
    ## Extraindo URL e iniciando o download       ##
    ################################################
    video_url = extract_video_url(config_text)
    if video_url:
        print(f"URL do vídeo encontrada: {video_url}")
        download_video(video_url, output_name)
    else:
        print("Nenhuma URL válida foi encontrada no conteúdo do arquivo.")
except FileNotFoundError:
    print("Arquivo 'media.txt' não encontrado. Verifique se está no mesmo diretório do script.")
