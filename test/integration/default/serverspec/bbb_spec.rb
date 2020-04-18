require 'serverspec'

# Required by serverspec
set :backend, :exec

pkg_list = [ 'mongodb-org', 'bbb-check', 'bbb-html5', 'bigbluebutton' ]

for p in pkg_list do
  describe package("#{p}"), :if => os[:family] == 'ubuntu' || os[:family] == 'debian'  do
    it { should be_installed }
  end
end

describe service('bbb-html5') do
  it { should be_enabled }
  it { should be_running }
end
describe service('bbb-webrtc-sfu') do
  it { should be_enabled }
  it { should be_running }
end
describe service('bbb-web') do
  it { should be_enabled }
  it { should be_running }
end

describe process("node") do
  #its(:user) { should eq "bigbluebutton" }
  # its(:args) { should match /server.js/ }
  its(:count) { should eq 7 }
end

describe port(9001) do
  it { should be_listening.with('tcp') }
end
describe port(3010) do
  it { should be_listening.with('tcp') }
end

describe command('curl -vk https://localhost') do
  its(:stdout) { should match /BigBlueButton - Open Source Web Conferencing/ }
  its(:stdout) { should match /Welcome Message & Login Into Demo/ }
  its(:stderr) { should match /200 OK/ }
  its(:stderr) { should_not match /No such file or directory/ }
  its(:exit_status) { should eq 0 }
end
