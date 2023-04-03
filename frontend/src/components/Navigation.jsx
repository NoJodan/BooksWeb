import Link from "next/link";
import { useState, useEffect } from "react";

const API = process.env.NEXT_PUBLIC_API;

export const Navigation = () => {
  const [search, setSearch] = useState("");

  const [token_expired, setTokenExpired] = useState(false);
  const [jwt, setJwt] = useState(undefined);

  const handleSearch = (e) => {
    e.preventDefault();
  };

  const getTokenData = async () => {
    const token = localStorage.token;
    setJwt(token);
    const headers =
      token === undefined
        ? {}
        : {
            Authorization: `Bearer ${token}`,
          };
    const res = await fetch(`${API}/others/check-jwt`, {
      method: "GET",
      headers: headers,
    });
    const json = await res.json();
    setTokenExpired(json.data === undefined ? false : json.data.is_expired);
  };

  useEffect(() => {
    getTokenData();
  }, [jwt, token_expired]);

  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container-lg">
          <Link className="navbar-brand" href="/">
            Books Web
          </Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <Link className="nav-link" href="#">
                  Features
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" href="/about">
                  About
                </Link>
              </li>
            </ul>

            <form className="d-flex">
              <input
                className="form-control me-sm-2"
                type="search"
                placeholder="Search"
                onChange={(e) => setSearch(e.target.value)}
                value={search}
              />
              <button className="btn btn-secondary my-2 my-sm-0" type="submit">
                Search
              </button>
            </form>

            <ul className="navbar-nav mx-1">
              {token_expired || jwt === undefined ? (
                <>
                  <li className="nav-item">
                    <Link className="nav-link" href="/signup">
                      Sign up
                    </Link>
                  </li>
                  <li className="nav-item mx-1">
                    <Link className="nav-link" href="/login">
                      Login
                    </Link>
                  </li>
                </>
              ) : (
                <li className="nav-item mx-1">
                  <button
                    className="btn btn-primary"
                    type="button"
                    onClick={(e) => {
                      e.preventDefault();
                      localStorage.removeItem("token");
                      setJwt(undefined);
                    }}
                  >
                    Logout
                  </button>
                </li>
              )}
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
};
