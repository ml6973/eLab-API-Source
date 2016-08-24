#cloud-config
users:
  - name: ryan
    ssh-authorized-keys:
      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDNWdWGtuH05mk1tzQjNnAugK0SrDxkE4eXPiOaf6OY8d5mdv+awNPL5TbtE/eyA4L657w+et54+2wCLEUXaKddoPC5w847RA3zaKw7AS2KqlwWtcLd7GykVeiJck/K3sgJfYu1sJCQY9v0rdviz78KF8nARakLNz+5Q0hcWeFuIOUBoGvDsaiLysSD5aurcc3iLWUMub6tkd0v/pRoNhJ2K3VZFlTat6EUodYJk+5WuEdAjj5t/8jNGOJzrerVPNAbv4cJYT3+EoR+rL5cWHBF77ePYZSlFTfAtfpKn2FIF3d6PgU5JzoUzo8T24HxFGPdd/VFMNvIuw/wnVm6Urhd ryan@Ryans-MacBook-Pro.local
    groups: sudo
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    lock-passwd: False
    passwd: $6$K4FQ8CCCF6aFB04D$M3K4WxZkjaM4lK5BhhLI6F3s3flxdLcmKZijoooYG6qgs4w.6tysH0mr0z0HtCWLboBiCJNjMaB2hkbvEcdDE0
runcmd:
  - touch /home/ryan/testfile.txt
  - [ sudo, sed, -i, 's/[#]*PasswordAuthentication no/PasswordAuthentication yes/g', /etc/ssh/sshd_config ]
  - sudo service ssh restart
