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

function App() {
  const [count, setCount] = useState(0)

const router = createBrowserRouter(
      createRoutesFromElements(
        <Route path='/' element={<MainLayout />}> 
           <Route index element={<Dashboard />} />
           <Route path='/aircraftlist' element={<AircraftList />} />
           <Route path='/assignmentlist' element={<AssignmentList />} />
           <Route path='/addaircraft' element={<AddAircraftPage />} />
           <Route path='*' element={<NotFoundPage />} />

{/* 
          <Route path='/' element={<AddJobPage addJobSubmit={addJob} />} />
          <Route
            path='/edit-job/:id'
            element={<EditJobPage updateJobSubmit={updateJob} />}
            loader={jobLoader}
          />
          <Route
            path='/jobs/:id'
            element={<JobPage deleteJob={deleteJob} />}
            loader={jobLoader}
          /> */}
            
        </Route>
      )
    );

    return <RouterProvider router={router} />;

}

export default App
