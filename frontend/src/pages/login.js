import { Container } from "@/components/Container";
import { Checkbox } from "@/components/Checkbox";
import { useRouter } from 'next/router';
import { useState } from "react";


const API = process.env.NEXT_PUBLIC_API


const Login = () => {
    const router = useRouter();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [stayLogged, setStayLogged] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const payload = btoa(`${username}:${password}`);
   
        const options = {
            params:{
                stay_logged_in: stayLogged ? "true" : "false"
            },
            method: 'GET',
            headers: {
                'Authorization': `Basic ${payload}`
            }
        }
        const response = await fetch(`${API}/users/login`, options);
        const data = await response.json();
        localStorage.setItem('token', data.data.token);
        await router.push('/');
    }

    return (
    <>
        <Container className="d-flex justify-content-center" title="Login">
            
            <div className="card login-card my-5">
                <div className="card-title">
                    <h1>
                        Login
                    </h1>
                </div>
                <div className="card-body">
                    <form onSubmit={handleSubmit}>
                        <label htmlFor="username">
                            Username
                        </label>
                        <input
                            className="form-control my-2"
                            type="text"
                            name="username"
                            placeholder="Username"
                            onChange={(e) => setUsername(e.target.value)}
                        />
                        <label htmlFor="password">
                            Password
                        </label>
                        <input
                            className="form-control my-2"
                            type="password"
                            name="password"
                            placeholder="Password"
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <Checkbox label="Stay logged in" onChange={(e) => setStayLogged(e.target.checked)} />
                        <button className="my-1 btn btn-primary" type="submit">
                            Login
                        </button>
                    </form>
                </div>
            </div>

        </Container>
    </>
    )

}

export default Login;