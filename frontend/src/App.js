import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import {About} from './components/About'
import {Admin} from './components/Admin'
import {Navbar} from './components/Navbar'

export default function App() {
	return (
		<Router>
			<Navbar/>
			<div className="container p-2">
				<Routes>
					<Route path='/about' element={<About/>} />
					<Route path='/admin' element={<Admin/>} />
				</Routes>
			</div>
		</Router>
	)
}