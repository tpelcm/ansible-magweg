# -*- mode: ruby -*-
# vi: set ft=ruby :

vagrant_box = 'generic/centos7'

# vpass file for Ansible vault secrets.yml
vpass_file = File.join(File.dirname(__FILE__), 'vpass')

# Vagrant nodes
nodes = {}
nodes['sonarqube'] = { 'ip' => '1.1.1.4', 'plays' => %w[sonarqube], 'memory' => 1024 * 4 }
nodes['db'] = {  'ip' => '1.1.1.2', 'plays' => %w[postgresql] }
nodes['proxy'] = {  'ip' => '1.1.1.3', 'plays' => %w[devproxy], 'data-disk' => true }
nodes['awx'] = { 'ip' => '1.1.1.5', 'plays' => %w[awx], 'memory' => 1024 * 4, 'cpus' => 4, 'data-disk' => true }
nodes['nexus'] = { 'ip' => '1.1.1.7', 'plays' => %w[nexus], 'memory' => 1024 * 4, 'cpus' => 4 }
nodes['jenkins'] = { 'ip' => '1.1.1.9', 'plays' => %w[jenkins], 'memory' => 1024 * 4 }
nodes['sites'] = { 'ip' => '1.1.1.10', 'plays' => %w[sites] }
nodes['bitbucket'] = {  'ip' => '1.1.1.11', 'plays' => %w[bitbucket], 'memory' => 1024 * 4, 'data-disk' => true }
nodes['confluence'] = { 'ip' => '1.1.1.12', 'plays' => %w[confluence], 'memory' => 1024 * 4, 'data-disk' => true }
nodes['jira'] = { 'ip' => '1.1.1.13', 'plays' => %w[jira], 'memory' => 1024 * 4, 'data-disk' => true }
nodes['bastion'] = { 'ip' => '1.1.1.14', 'plays' => %w[desktop], 'memory' => 1024 * 4, 'data-disk' => true }
nodes['oracle'] = {  'ip' => '1.1.1.15', 'plays' => %w[oracle], 'memory' => 1024 * 4, 'data-disk' => true }
nodes['myapp'] = { 'ip' => '1.1.1.5', 'plays' => %w[myapp], 'data-disk' => true }
# nodes['myapp2'] = { 'ip' => '1.1.1.6', 'plays' => %w(myapp), 'data-disk' => true }

Vagrant.configure(2) do |config|
  config.vm.synced_folder '.', '/vagrant'
  nodes.each do |n, a|
    bx = a['box'] || vagrant_box
    # unless vm_exists? n
    #  shell_provision = 'sudo apt-get update && sudo apt-get -y install python'
    #  shell_provision = 'sudo yum update -y && sudo yum -y install python && echo PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin | sudo tee /etc/environment > /dev/null' if bx.include? 'centos'
    # end
    config.vm.define n do |cfg|
      cfg.vm.hostname = n # .e.g. sonarqube
      cfg.vm.box = bx
      cfg.vm.network 'private_network', ip: a['ip']
      cfg.vm.provider 'virtualbox' do |vb|
        vb.gui = false
        vb.memory = a['memory'] || 1024
        vb.cpus = a['cpus'] || 2
        add_disk(vb, 1, 120 * 1024, "cicd-data-#{n}.vdi", 'IDE Controller') if a['data-disk'] == true
      end
      # cfg.vm.provision 'shell', inline: shell_provision if shell_provision
      plays = ENV['PLAY'] ? [ENV['PLAY']] : a['plays']
      plays.each do |p|
        cfg.vm.provision 'ansible' do |ansible|
          ansible.config_file = 'ansible.cfg'
          ansible.playbook = "plays/#{p}.yml"
          ansible.compatibility_mode = '2.0'
          ansible.inventory_path = 'development.ini'
          # ansible.host_vars = ansible_host_vars
          # ansible.galaxy_role_file = '../roles/requirements.yml'
          # ansible.galaxy_roles_path = '~/.ansible/roles'
          # ansible.verbose = 'vvv'
        end
      end
    end
  end
end

File.open(vpass_file, 'w') { |f| f.write('secret') } unless File.exist? vpass_file

def add_disk(vb_provider, port = 2, size = 120 * 1024, filename = nil, controller = 'IDE Controller')
  filename = "disk#{port}.vdi" if filename.nil?
  disk = File.expand_path(filename)
  vb_provider.customize ['createhd', '--filename', disk, '--format', 'VDI', '--size', size] unless File.exist?(disk)
  vb_provider.customize ['storageattach', :id, '--storagectl', controller, '--port', port, '--device', 0, '--type', 'hdd', '--medium', disk]
end

def vm_exists?(vm_name = 'default', provider = 'virtualbox')
  File.exist?(File.join(File.dirname(__FILE__), ".vagrant/machines/#{vm_name}/#{provider}/vagrant_cwd"))
end
