import Link from "next/link";
import { useState, useEffect } from "react";


const API = process.env.NEXT_PUBLIC_API;

export const Navigation = () => {
    
    const [token_expired, setTokenExpired] = useState(false);
    const [token, setToken] = useState(localStorage.token);

    const getTokenData = async () => {
        const token = localStorage.token;
        const headers = token === undefined ? {} : {
            'Authorization': `Bearer ${token}`
        }
        const res = await fetch(`${API}/others/check-jwt`, {
            method: 'GET',
            headers: headers
        });
        const json = await res.json();
        setTokenExpired(json.data === undefined ? false : json.data.is_expired);
    }

    useEffect(() => {
        getTokenData();
    }, [token,token_expired]);

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
            <div className="container-lg">
                <Link className="navbar-brand" href="/">Books Web</Link>
                <div className="collapse navbar-collapse">
                    <ul className="navbar-nav me-auto">
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
                        />
                        <button
                            className="btn btn-secondary my-2 my-sm-0"
                            type="submit">
                            Search
                        </button>
                    </form>
                    
                    <ul className="navbar-nav mx-1">
                        {
                        token_expired || token === undefined ? (
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
                        ): 
                        (<li className="nav-item mx-1">
                            <button className="btn btn-primary" type="button" onClick={(e) => {
                                e.preventDefault();
                                localStorage.removeItem('token');
                                setToken(undefined);
                            }} >Logout</button>
                        </li>)
                        
                        }
                    </ul>
                    
                </div>
            </div>
        </nav>
    )
}