Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.network "forwarded_port", guest: 4000, host: 4000 # Firestore Emulator UI
  config.vm.network "forwarded_port", guest: 8081, host: 8081 # Firestore Emulator API
  config.vm.network "forwarded_port", guest: 9150, host: 9150 # Firestore Emulator WebSocket
  config.vm.network "forwarded_port", guest: 8000, host: 8000 # FastAPI
  config.vm.network "forwarded_port", guest: 8080, host: 8080 # Vue.js Dev Server
  config.vm.synced_folder ".", "/vagrant" # Syncs your project folder to /vagrant_data in the VM
end
