import React from 'react';
import { render } from 'react-dom'
import { Router, Route, Link, browserHistory } from 'react-router'


const App = React.createClass({
  render() {
      return (
        <div>
          <header>
            <div className="container flex-row-space-between">
              <h1>
                <a href="/">gitPlaylists</a>
              </h1>
              <nav className="material-tabs">
                <a Link to="/about">Login</a>
                <a Link to="/about">Sign up</a>
              </nav>
            </div>
          </header>
          <main>
            <div className="container">Hello world</div>
          </main>
          <footer className="container">
            <hr/>
            <span>
              FOOTER
            </span>
          </footer>
        </div>,
      )
  }
});

const About = React.createClass({
  render() {
      return (
        <div>About</div>,
      )
  }
});

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
      </div>
    )
  }
});

const NoMatch = React.createClass({
  render() {
      return (
        <div>404?</div>,
      )
  }
});

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
), document.getElementById("content"))
