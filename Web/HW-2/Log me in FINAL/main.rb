require 'sinatra'
require 'mysql2'

db = Mysql2::Client.new(host: 'mysql', username: 'root', password: 'pa55w0rd', database: 'db')

def sqli_waf (str)
    str.gsub(/union|select|where|and|or| |=/i, '')
end

def addslashes (str)
    str.gsub(/['"]/,'\\\\\0')
end

get '/' do
    p %{
    <h1>Log me in: Final</h1>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="guest">
        <input type="password" name="password" placeholder="guest">
        <button>Login</button>
    </form>
    }
end

post '/login' do
    @params = Hash[params.map { |key, value| [key, sqli_waf(value)] }]
    query = "SELECT * FROM users WHERE username='#{addslashes(@params['username'])}' and password='#{addslashes(@params['password'])}'"
    result = db.query(query).first
    if result
        "Welcome!"
    else
        "Incorrect username or password."
    end
end
