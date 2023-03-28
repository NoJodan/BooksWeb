import { Container } from "@/components/Container";
import { Checkbox } from "@/components/Checkbox";
import { useRouter } from 'next/router';
import { useState } from "react";


const API = process.env.NEXT_PUBLIC_API


const Signup = () => {
    const router = useRouter();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");
    const [stayLogged, setStayLogged] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (password !== password2) {
            setPassword2("");
            alert("Passwords do not match");
            return;
        }

        
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        }
        const response = await fetch(`${API}/users/register`, options);
        const data = await response.json();
        if (data.status.name === 'data_conflict') {
            alert(data.msg);
            return;
        }
        const payload = btoa(`${username}:${password}`);
   
        const options2 = {
            params:{
                stay_logged_in: stayLogged ? "true" : "false"
            },
            method: 'GET',
            headers: {
                'Authorization': `Basic ${payload}`
            }
        }
        const response2 = await fetch(`${API}/users/login`, options2);
        const data2 = await response2.json();
        localStorage.setItem('token', data2.data.token);
        

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
                            value={username}
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
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <label htmlFor="password2">
                            Confirm Password
                        </label>
                        <input
                            className="form-control my-2"
                            type="password"
                            name="password2"
                            placeholder="Confirm password"
                            value= {password2}
                            onChange={(e) => setPassword2(e.target.value)}
                        />
                        <Checkbox label="Stay logged in" onChange={(e) => setStayLogged(e.target.checked)} />
                        <button className="my-1 btn btn-primary" type="submit">
                            Sign up
                        </button>
                    </form>
                </div>
            </div>

        </Container>
    </>
    )

}

export default Signup;