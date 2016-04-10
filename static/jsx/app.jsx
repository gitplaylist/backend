React.render(
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
