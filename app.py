import sam

app = sam.create_app()

if __name__ == "__main__":
    if app.debug: app.run(host='0.0.0.0') # Executa no host local e LAN, para testar em vários dispositivos na mesma rede.
    else: app.run()