from django import template

from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.template import loader
import paramiko

from page1.forms import consol

from mcrcon import MCRcon
from mctools import QUERYClient
import socket
# Create your views here.

###Connexion SSH au RPI4-------------------------------------->>>
hostname = "rpi4"
host = socket.gethostbyname(hostname)
port = 22
username = "pi"
password = "aloxsg1!r"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

def sshCommand(command:str):
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    return lines

def consolInput(input:str):
    mcr = MCRcon("rpi4", "aloxsg1!r")
    mcr.connect()
    resp = mcr.command(input)
    print(resp)
    mcr.disconnect()

def getStats(host):
    query = QUERYClient(host)

    stats = query.get_full_stats()
    return stats

"""
def namePlayerTraitement(name):
    str = ''
    for i in range(len(name)):
        if name[i] =! :
            str = str + name[i]
              
        else:
            return str
"""            



def pageOne(request):
    
###Recuperation des logs--------------------------->>>

    log = sshCommand("cat /opt/minecraft/logs/latest.log")

###Traitement des logs----------------------------->>>

   
###Traitement de la réponse HTTP------------------->>>

    ###Consol_Formulaire--------------------------->>>
    
    #print('La méthode de requête est : ', request.method)
    #print('Les données POST sont : ', request.POST)
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = consol(request.POST)
        
        if form.is_valid():#Action lorsque le formulaire et valide
            #form.cleaned_data est un dict contenant les données du formulaire après qu'elles
            #ont subi le processus de validation.
            #Lorsque nous sommes prêts à faire quelque chose avec les données de notre formulaire,
            #nous pouvons accéder à chacun des champs via form.cleaned_data['name_of_field'],
            #mais nous devons d'abord appeler form.is_valid().
            
            #theCommand = form.cleaned_data['command']
            consolInput(form.cleaned_data['command'])
            redirect("http://127.0.0.1:8000/pageRedirect/")
            #consolInput(theCommand)
            #theCommand = ""
            #######FONCTIONNE PAS##############
            #consolInput("say toi la")
    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = consol()
    
    form = consol()
    
    template = loader.get_template("pageOne.html")
    
    stats = getStats(host)
    listPlayers = stats['players']
    
    
    
    
    maxPlayers = stats['maxplayers']
    numPlayers = stats['numplayers']
    print(len(listPlayers))
        
    
        
    
    
    firstPlayer = 'tulipe'
    secondPlayer = 'velo'
    context = {"logs" : log,
               "form" : form,
               "numPlayers" : numPlayers,
               "maxPlayers" : maxPlayers,
               "listPlayers" : listPlayers,
               "firstPlayer" : firstPlayer,
               "secondPlayer" : secondPlayer}

###Renvoi la réponse HTTP-------------------------->>>
    
    return HttpResponse(template.render(context,request))
    
    

        
    
    
    
    
    
def pageTwo(request):
    shops = ("Auchan","Super U","Intermarché")
    context = {"shops" : shops}
    template = loader.get_template("pageTwo.html")
    return HttpResponse(template.render(context,request))


def pageRedirect(request):
    return redirect("http://127.0.0.1:8000/pageOne/")

def TurnOffPiButton(request):
    sshCommand("sudo shutdown -h now")
    return HttpResponse("""<html><script>window.location.replace('/pageOne/');</script></html>""")

def TurnOffMcButton(request):
    consolInput("stop")
    return HttpResponse("""<html><script>window.location.replace('/pageOne/');</script></html>""")

def TurnOnMcButton(request):
    sshCommand("/opt/scripts/minecraftStart.sh")
    return HttpResponse("""<html><script>window.location.replace('/pageOne/');</script></html>""")

def TimeSetDayButton(request):
    consolInput("time set 0")
    return HttpResponse("""<html><script>window.location.replace('/pageOne/');</script></html>""")

def TimeSetNightButton(request):
    consolInput("time set night")
    return HttpResponse("""<html><script>window.location.replace('/pageOne/');</script></html>""")

def WeatherButton(request):
    consolInput("weather clear")
    return HttpResponse("""<html><script>window.location.replace('/pageOne/');</script></html>""")


    
    
