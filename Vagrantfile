Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.network "forwarded_port", guest: 8000, host: 8000 # FastAPI
  config.vm.network "forwarded_port", guest: 8080, host: 8080 # Vue.js Dev Server
  config.vm.synced_folder ".", "/vagrant" # Syncs your project folder to /vagrant_data in the VM
end
