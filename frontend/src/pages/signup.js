import { Container } from "@/components/Container";
import { Checkbox } from "@/components/Checkbox";
import { useRouter } from 'next/router';
import { useState } from "react";


const API = process.env.NEXT_PUBLIC_API


const Signup = () => {
    const router = useRouter();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
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
                password: password,
                email: email
            })
        }
        const response = await fetch(`${API}/users`, options);
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
        const response2 = await fetch(`${API}/users`, options2);
        const data2 = await response2.json();
        localStorage.setItem('token', data2.data.token);
        

        await router.push('/');
    }

    return (
    <>
        <Container className="d-flex justify-content-center" title="Login">
            <div className="container h-100 mt-5">
                <div className="row d-flex justify-content-center align-items-center h-100">
                    <div className="col-lg-12 col-xl-11">
                        <div className="card text-black" style={{ borderRadius: '25px' }}>
                            <div className="card-body p-md-5">
                                <div className="row justify-content-center">
                                    <div className="col-md-10 col-lg-6 col-xl-5 order-2 order-lg-1">
                                        <p className="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">Sign up</p>
                                        <form className="mx-1 mx-md-4" onSubmit={handleSubmit}>
                                            <div className="d-flex flex-row align-items-center mb-4">
                                                <i className="fas fa-user fa-lg me-3 fa-fw"></i>
                                                <div className="form-outline flex-fill mb-0">
                                                    <input type="text" name="username" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} id="form3Example1c" className="form-control" />
                                                </div>
                                            </div>
                                            <div className="d-flex flex-row align-items-center mb-4">
                                                <i className="fas fa-envelope fa-lg me-3 fa-fw"></i>
                                                <div className="form-outline flex-fill mb-0">
                                                    <input type="email" placeholder="Your Email" value={email} onChange={(e) => setEmail(e.target.value)} id="form3Example3c" className="form-control" />
                                                </div>
                                            </div>
                                            <div className="d-flex flex-row align-items-center mb-4">
                                                <i className="fas fa-lock fa-lg me-3 fa-fw"></i>
                                                <div className="form-outline flex-fill mb-0">
                                                    <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} id="form3Example4c" className="form-control" />
                                                </div>
                                            </div>
                                            <div className="d-flex flex-row align-items-center mb-4">
                                                <i className="fas fa-key fa-lg me-3 fa-fw"></i>
                                                <div className="form-outline flex-fill mb-0">
                                                    <input type="password" placeholder="Repeat your password" value={password2} onChange={(e) => setPassword2(e.target.value)} id="form3Example4cd" className="form-control" />
                                                </div>
                                            </div>
                                            <div className="form-check d-flex justify-content-center mb-5">
                                                <Checkbox label="Stay logged in" onChange={(e) => setStayLogged(e.target.checked)} />
                                            </div>
                                            <div className="d-flex justify-content-center mx-4 mb-3 mb-lg-4">
                                                <button type="submit" className="btn btn-primary btn-lg">Register</button>
                                            </div>
                                        </form>
                                    </div>
                                    <div className="col-md-10 col-lg-6 col-xl-7 d-flex align-items-center order-1 order-lg-2">
                                        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-registration/draw1.webp"
                                        className="img-fluid" alt="Sample image"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Container>
    </>
    )

}

export default Signup;