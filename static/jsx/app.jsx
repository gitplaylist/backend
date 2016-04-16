import React from 'react';
import { render } from 'react-dom'
import { Router, Route, Link, browserHistory } from 'react-router'


class App extends React.Component {
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
}

class AboutView extends React.Component {
  render() {
      return (
        <div>About</div>,
      )
  }
}

class UserListView extends React.Component {
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
}

class UserView extends React.Component {
  componentDidMount() {
    this.setState({
      // route components are rendered with useful information, like URL params
      user: findUserById(this.props.params.userId)
    })
  }

  render() {
    return (
      <div>
        <h2>{this.state.user.name}</h2>
      </div>
    )
  }
}

class NoMatchView extends React.Component {
  render() {
      return (
        <div>404?</div>,
      )
  }
}

render((
  <Router history={browserHistory}>
    <Route path="/" component={App}>
      <Route path="about" component={AboutView}/>
      <Route path="users" component={UserListView}>
        <Route path="/user/:userId" component={UserView}/>
      </Route>
      <Route path="*" component={NoMatchView}/>
    </Route>
  </Router>
), document.getElementById("content"))
