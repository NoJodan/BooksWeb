import React from "react";
import { Link } from "react-router-dom";

export const Navbar = () => (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container-lg">
            <Link className="navbar-brand" to="/">
                Books Web
            </Link>
            <button
                className="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarColor01"
                aria-controls="navbarColor01"
                aria-expanded="false"
                aria-label="Toggle navigation">
                <span className="navbar-toggler-icon" />
            </button>
            <div className="collapse navbar-collapse" id="navbarColor01">
                <ul className="navbar-nav me-auto">
                    <li className="nav-item">
                        <Link className="nav-link" to="#">
                            Features
                        </Link>
					</li>
                    <li className="nav-item">
                        <Link className="nav-link" to="/about">
                            About
                        </Link>
                    </li>
                </ul>
                <form className="d-flex">
                    <input
                        className="form-control me-sm-2"
                        type="search"
                        placeholder="Search"
                    />
                    <button
                        className="btn btn-secondary my-2 my-sm-0"
                        type="submit">
                        Search
                    </button>
                </form>
            </div>
        </div>
    </nav>
);
