import React from 'react';
import { render } from 'react-dom'
import { Router, Route, Link, IndexRoute, browserHistory } from 'react-router';
import IndexView from './components/index.jsx';
import AboutView from './components/about.jsx';
import NoMatchView from './components/nomatch.jsx';
import UserView from './components/user.jsx';
import UserListView from './components/userlist.jsx';


class App extends React.Component {
  render() {
      return (
        <div>
          <header>
            <div className="container flex-row-space-between">
              <h1>
                <Link to="/">gitPlaylists</Link>
              </h1>
              <nav className="material-tabs">
                <Link to="/about">Login</Link>
                <Link to="/about">Sign up</Link>
              </nav>
            </div>
          </header>
          <main>
            {this.props.children}
          </main>
          <footer className="container">
            <hr/>
            <span>
              FOOTER
            </span>
          </footer>
        </div>
      )
  }
}


const router =(<Router history={browserHistory}>
  <Route path="/" component={App}>
    <IndexRoute component={IndexView} />
    <Route path="about" component={AboutView} />
    <Route path="*" component={NoMatchView} />
  </Route>
</Router>);

render(router, document.getElementById("content"));
