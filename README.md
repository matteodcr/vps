[![Vagrant](https://img.shields.io/badge/Vagrant-blue?logo=vagrant)](https://www.vagrantup.com/)
[![Ansible](https://img.shields.io/badge/Ansible-green?logo=ansible)](https://www.ansible.com/)
[![KVM](https://img.shields.io/badge/KVM-red?logo=linux)](https://www.linux-kvm.org/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-blue?logo=kubernetes)](https://k3s.io/)

# Setup VPS

Ce dépôt contient toutes les ressources nécessaires pour configurer une machine distante afin d'héberger un cluster Kubernetes k3s :
- **Setup virtuel KVM avec Vagrant** : disponible dans le dossier [`/vagrant`](./vagrant). Cette VM servira pour les tests des scripts Ansible
- **Fichiers Ansible** : tous les fichiers nécessaires pour automatiser la configuration de la machine se trouvent dans le dossier [`/ansible`](./ansible).

## Setup rapide
### Prérequis
- **Vagrant avec KVM** : [Télécharger Vagrant](https://www.vagrantup.com/downloads)
- **Ansible** : [Guide d'installation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

### Étapes
1. **Démarrer la VM**  
    Exécutez la commande suivante pour démarrer la machine virtuelle :  
    ```bash
    vagrant up
    ```

2. **Exécuter un playbook de base**  
    Lancez le playbook Ansible pour effectuer une configuration initiale :  
    ```bash
    ansible-playbook playbooks/base-setup.yml -i inventory/vm.py
    ```

### Notes
- Pour l'instant, fonctionne uniquement sur Linux

