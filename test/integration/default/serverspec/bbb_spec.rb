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
  its(:user) { should eq "bigbluebutton" }
  its(:args) { should match /server.js/ }
  its(:count) { should eq 1 }
end
describe process("node") do
  its(:user) { should eq "bigbluebutton" }
  its(:args) { should match /\.\/lib\/video\/VideoProcess.js/ }
  its(:count) { should eq 1 }
end
describe process("node") do
  its(:user) { should eq "bigbluebutton" }
  its(:args) { should match /\.\/lib\/audio\/AudioProcess.js/ }
  its(:count) { should eq 1 }
end

describe port(9001) do
  it { should be_listening.with('tcp') }
end
describe port(3010) do
  it { should be_listening.with('tcp') }
end
