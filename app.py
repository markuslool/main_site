from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def _is_local_host(hostname: str) -> bool:
    """Return True if hostname corresponds to a localhost address."""
    # hostname may include port (e.g. "localhost:5000"), so strip it.
    hostname = hostname.split(":")[0]
    return hostname in {"localhost", "127.0.0.1", "::1"}

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.before_request
def redirect_to_https():
    """
    Redirect to HTTPS when appropriate.

    - If the request appears secure (either via request.is_secure or via the
      common `X-Forwarded-Proto` header set by proxies), do nothing.
    - Do not redirect when the host is localhost/127.0.0.1/::1 to avoid breaking
      local development.
    - Otherwise, perform a 301 redirect to the HTTPS version of the current URL.
    """
    # Skip redirect on local development hosts
    host = request.host or ""
    if _is_local_host(host):
        return None

    # Check common proxy header first, falling back to request.is_secure
    xfp = request.headers.get("X-Forwarded-Proto", "")
    if xfp:
        is_secure = xfp.split(",")[0].strip() == "https"
    else:
        is_secure = request.is_secure

    if not is_secure:
        # Build the HTTPS URL safely: only replace the scheme portion once.
        url = request.url
        if url.startswith("http://"):
            url = "https://" + url[len("http://") :]
        else:
            # As a fallback, construct from components
            url = request.url.replace("http:", "https:", 1)
        return redirect(url, code=301)

    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/first")
def first():
    return render_template("first.html")


@app.route("/second")
def second():
    return render_template("second.html")


@app.route("/third")
def third():
    return render_template("third.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    # When running locally, binding to 127.0.0.1:5000 is fine; the before_request
    # guard prevents HTTPS redirects for localhost.
    app.run(host="127.0.0.1", port=5000, debug=False)
