# Ansibley-Python

Combinamos Ansible y Python para automatizar el despliegue de la aplicación System Monitor en servidores.
La app recopila información de hardware y procesos, la expone vía API HTTP y la envía a una base de datos. 
Con Ansible, se instala Python, se crea un entorno virtual, se copian los archivos y se configura la app como un servicio systemd, asegurando que se ejecute automáticamente y se mantenga activo.

## 📁 Archivos de Configuración

### `ansible.cfg`
Configuración principal de Ansible:
```ini
[defaults]
remote_tmp = /tmp/.ansible/tmp        # Directorio temporal en los hosts remotos
roles_path = ./roles                  # Ruta donde se encuentran los roles
host_key_checking = False             # Desactiva la verificación de llaves SSH
```

### `flask.service.j2`
Plantilla systemd para ejecutar la app Flask como servicio:
```ini
[Unit]
Description=System Monitor Flask API
After=network.target

[Service]
User={{ ansible_user }}
WorkingDirectory=/opt/system_monitor
Environment="PATH=/opt/system_monitor/venv/bin"
Environment="MONGO_URI=mongodb://192.168.18.3:27017/system_monitor"
ExecStart=/opt/system_monitor/venv/bin/python /opt/system_monitor/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### `inventories/hosts.ini`
Archivo de inventario que lista los hosts y grupos de servidores gestionados. Define la estructura de la infraestructura y las conexiones SSH.

### `playbooks/`
Contiene los playbooks de Ansible (.yml) con las tareas y roles a ejecutar en los hosts. Define qué configuraciones aplicar y en qué orden.

### `roles/`
Directorio con roles reutilizables. Cada rol contiene tareas, handlers, templates y archivos organizados para funcionalidades específicas.

### `requirements.txt`
Lista las dependencias Python necesarias (ansible, paramiko, jinja2, etc.) para ejecutar el proyecto.


##  Despliegue

### Ejecutar el playbook de despliegue
```bash
ansible-playbook -i inventories/hosts.ini playbooks/deploy.yml --ask-pass --ask-become-pass
```

**Resultado del despliegue:**

![Resultado deploy](https://github.com/user-attachments/assets/64bfe369-1aea-4bd4-abf8-00c50b03b678)

### Verificar el servicio

Una vez desplegado, puedes verificar que el servicio Flask está funcionando mediante una petición HTTP:

```bash
curl http://tu-servidor:5000/
```

**Resultado de la petición HTTP:**

![Resultado petición HTTP](https://github.com/user-attachments/assets/8acb3816-277d-4368-b09c-c7b1597dc6c5)


....
