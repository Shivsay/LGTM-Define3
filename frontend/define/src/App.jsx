import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Route, RouterProvider } from "react-router-dom";
import { createBrowserRouter,createRoutesFromElements } from "react-router-dom";
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import AircraftList from './pages/AircraftList';
import NotFoundPage from './components/NotFoundPage';
import AddAircraftPage from './pages/AddAircraftPage';
import AssignmentList from './pages/AssignmentList';
import AddFlightPage from './pages/AddFlightPage';

function App() {

const addNewAircraft = async (newAircraft) => {
    const res = await fetch('/api/put-aircraft', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newAircraft),
    });
    return;
  };

  const addNewFlight = async (newFlight) => {
    const res = await fetch('/api/put-flight', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newFlight),
    });
    return;
  };

const router = createBrowserRouter(
      createRoutesFromElements(
        <Route path='/' element={<MainLayout />}> 
           <Route index element={<Dashboard />} />
           <Route path='/aircraftlist' element={<AircraftList />} />
           <Route path='/assignmentlist' element={<AssignmentList />} />
           <Route path='/addaircraft' element={<AddAircraftPage addAircraftSubmit={addNewAircraft}/>} />
           <Route path='/addflight' element={<AddFlightPage addFlightSubmit={addNewFlight}/>} />
           <Route path='*' element={<NotFoundPage />} />
        </Route>
      )
    );

    return <RouterProvider router={router} />;

}

export default App
