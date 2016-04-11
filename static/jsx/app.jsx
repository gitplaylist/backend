import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, Link } from 'react-router'

const App = ReactDOM.createClass(
    <div>
      <header>
        <div class="container flex-row-space-between">
          <h1>
            <a href="/">gitPlaylists</a>
          </h1>
          <nav class="material-tabs">
            <a href="/">Login</a>
            <a href="/">Sign up</a>
          </nav>
        </div>
      </header>
      <main>
        <div class="container">Hello world</div>
      </main>
      <footer class="container">
        <hr/>
        <span>
          FOOTER
        </span>
      </footer>
    </div>,
    document.getElementById("content")
);
const About = ReactDOM.createClass(
    <div>      About
    </div>,
    document.getElementById("content")
);
const Users = React.createClass({
  render() {
    return (
      <div>
        <h1>Users</h1>
        <div className="master">
          <ul>
            {/* use Link to route around the app */}
            {this.state.users.map(user => (
              <li key={user.id}><Link to={`/user/${user.id}`}>{user.name}</Link></li>
            ))}
          </ul>
        </div>
        <div className="detail">
          {this.props.children}
        </div>
      </div>
    )
  }
});

const User = React.createClass({
  componentDidMount() {
    this.setState({
      // route components are rendered with useful information, like URL params
      user: findUserById(this.props.params.userId)
    })
  },

  render() {
    return (
      <div>
        <h2>{this.state.user.name}</h2>
        {/* etc. */}
      </div>
    )
  }
});
const NoMatch = ReactDOM.createClass(
    <div>
      About
    </div>,
    document.getElementById("content")
);

render((
  <Router history={browserHistory}>
    <Route path="/" component={App}>
      <Route path="about" component={About}/>
      <Route path="users" component={Users}>
        <Route path="/user/:userId" component={User}/>
      </Route>
      <Route path="*" component={NoMatch}/>
    </Route>
  </Router>
), document.body)
