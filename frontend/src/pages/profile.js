import { Container } from '@/components/Container'
import { useEffect, useState } from 'react'
import Image from "next/image";

const API = process.env.NEXT_PUBLIC_API

export default function Home() {
    const [profile, setProfile] = useState([])

    const getProfile = async () => {
        const token = localStorage.token;
        const headers = token === undefined ? {} : {
            'Authorization': `Bearer ${token}`
        }
        const options = {
            method: 'GET',
            headers: headers
        }
        const response = await fetch(`${API}/users/profile`, options)
        const info = await response.json()
        setProfile(info.data);
    }

    useEffect(() => {
        getProfile();
    }, []);
    return(
        <Container className="d-flex" title="Login">
            <div className="container">
                <div className="row d-flex justify-content-center align-items-center h-100">
                    <div className="col">
                        <div className="card">
                            <div className="text-white d-flex flex-row" style={{ backgroundColor: '#000000', height: '200px'}}>
                                <div className="ms-4 mt-5 d-flex flex-column" style={{ width: '150px' }}>
                                    {profile.image_b64 && <img src={`data:image/jpg;base64,${profile.image_b64}`}
                                        alt={profile.profile_image} className="img-fluid img-thumbnail mt-4 mb-2"
                                        style={{ width: '150px', zIndex: 1}}/>}
                                    <button type="button" className="btn btn-outline-dark" data-mdb-ripple-color="dark"
                                        style={{ zIndex: 1 }}>
                                        Edit profile
                                    </button>
                                </div>
                                <div className="ms-3" style={{ marginTop: '130px' }}>
                                    <h5>{profile.username}</h5>
                                    <p>{profile.created_at}</p>
                                </div>
                            </div>
                            <div className="p-4 text-black" style={{ backgroundColor: '#f8f9fa' }}>
                                <div className="d-flex justify-content-end text-center py-1">
                                    <div>
                                        <p className="mb-1 h5">253</p>
                                        <p className="small text-muted mb-0">Photos</p>
                                    </div>
                                <div className="px-3">
                                    <p className="mb-1 h5">1026</p>
                                    <p className="small text-muted mb-0">Followers</p>
                                </div>
                                <div>
                                    <p className="mb-1 h5">478</p>
                                    <p className="small text-muted mb-0">Following</p>
                                </div>
                                </div>
                            </div>
                            <div className="card-body p-4 text-black">
                                <div className="mb-5">
                                    <p className="lead fw-normal mb-1">About</p>
                                    <div className="p-4" style={{ backgroundColor: '#f8f9fa' }}>
                                        <p className="font-italic mb-1">Web Developer</p>
                                        <p className="font-italic mb-1">Lives in New York</p>
                                        <p className="font-italic mb-0">Photographer</p>
                                    </div>
                                </div>
                                <div className="d-flex justify-content-between align-items-center mb-4">
                                    <p className="lead fw-normal mb-0">Recent photos</p>
                                    <p className="mb-0"><a href="#!" className="text-muted">Show all</a></p>
                                </div>
                                <div className="row g-2">
                                    <div className="col mb-2">
                                        <img src="https://mdbcdn.b-cdn.net/img/Photos/Lightbox/Original/img%20(112).webp"
                                        alt="image 1" className="w-100 rounded-3"/>
                                    </div>
                                    <div className="col mb-2">
                                        <img src="https://mdbcdn.b-cdn.net/img/Photos/Lightbox/Original/img%20(107).webp"
                                        alt="image 1" className="w-100 rounded-3"/>
                                    </div>
                                </div>
                                <div className="row g-2">
                                    <div className="col">
                                        <img src="https://mdbcdn.b-cdn.net/img/Photos/Lightbox/Original/img%20(108).webp"
                                        alt="image 1" className="w-100 rounded-3"/>
                                    </div>
                                    <div className="col">
                                        <img src="https://mdbcdn.b-cdn.net/img/Photos/Lightbox/Original/img%20(114).webp"
                                        alt="image 1" className="w-100 rounded-3"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Container>
    )
}