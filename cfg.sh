#cloud-config
users:
  - name: ryan
    ssh-authorized-keys:
      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDNWdWGtuH05mk1tzQjNnAugK0SrDxkE4eXPiOaf6OY8d5mdv+awNPL5TbtE/eyA4L657w+et54+2wCLEUXaKddoPC5w847RA3zaKw7AS2KqlwWtcLd7GykVeiJck/K3sgJfYu1sJCQY9v0rdviz78KF8nARakLNz+5Q0hcWeFuIOUBoGvDsaiLysSD5aurcc3iLWUMub6tkd0v/pRoNhJ2K3VZFlTat6EUodYJk+5WuEdAjj5t/8jNGOJzrerVPNAbv4cJYT3+EoR+rL5cWHBF77ePYZSlFTfAtfpKn2FIF3d6PgU5JzoUzo8T24HxFGPdd/VFMNvIuw/wnVm6Urhd ryan@Ryans-MacBook-Pro.local
    groups: sudo
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    lock-passwd: False
    passwd: $6$teBLUH9EnBn0CDZk$VX4sfAOauGnNZu/8w4HrMym2WNC3tcFtjoXsZQmG9uHAU2Bnmi77YPZNZt0MxyMrzuZu8X1/yhvETpuUFKSpe.
runcmd:
  - [ sed, -i, 's/[#]*PasswordAuthentication no/PasswordAuthentication yes/g', /etc/ssh/sshd_config]
  - service ssh restart