require 'serverspec'

# Required by serverspec
set :backend, :exec

pkg_list = [ 'mongodb-org', 'bbb-check', 'bbb-html5', 'bigbluebutton' ]

for p in pkg_list do
  describe package("#{p}"), :if => os[:family] == 'ubuntu' || os[:family] == 'debian'  do
    it { should be_installed }
  end
end

describe service('bbb-html5')
  it { should be_enabled }
  it { should be_running }
end
describe service('bbb-webrtc-sfu')
  it { should be_enabled }
  it { should be_running }
end
describe service('bbb-web')
  it { should be_enabled }
  it { should be_running }
end
