require 'serverspec'

# Required by serverspec
set :backend, :exec

pkg_list = [ 'bbb-freeswitch-core', 'bbb-freeswitch-sounds' ]

for p in pkg_list do
  describe package("#{p}"), :if => os[:family] == 'ubuntu' || os[:family] == 'debian'  do
    it { should be_installed }
  end
end

describe service('freeswitch') do
  it { should be_enabled }
  it { should be_running }
end

describe process("freeswitch") do
  its(:user) { should eq "freeswitch" }
  its(:args) { should match /-u freeswitch -g daemon -ncwait/ }
  its(:count) { should eq 1 }
end

describe port(8081) do
  it { should be_listening.with('tcp') }
end
describe port(8082) do
  it { should be_listening.with('tcp') }
end
describe port(5060) do
  it { should be_listening.with('tcp') }
end
describe port(5090) do
  it { should be_listening.with('tcp') }
end
