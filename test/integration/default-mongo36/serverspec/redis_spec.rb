require 'serverspec'

# Required by serverspec
set :backend, :exec

describe process("redis-server") do
  it { should be_running }
end

describe service('redis-server'), :if => os[:family] == 'ubuntu' || os[:family] == 'debian' do  
  it { should be_enabled }
  it { should be_running }
end
describe service('redis'), :if => os[:family] == 'redhat' do  
  it { should be_enabled }
  it { should be_running }
end
describe port(6379) do
  it { should be_listening.with('tcp') }
end

