import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
//import { toast } from 'react-toastify';

const AddAircraftPage = ({ addAircraftSubmit }) => {
  const [registration, setRegistration] = useState('');
  const [aircrafttype, setAircraftType] = useState('');
  const [seatingcapacity, setSeatingCapacity] = useState('');

  const navigate = useNavigate();

  const submitForm = (e) => {
    e.preventDefault();

    const newAircraft = {
      aircrafttype:aircrafttype,
      registration: registration,
      seatingcapacity: seatingcapacity
    };

    addAirlineSubmit(newAircraft);

    // toast.success('Aircraft Added Successfully');

    return navigate('/dashboard');
  };

  return (
    <section className='bg-indigo-50'>
      <div className='container m-auto max-w-2xl py-24'>
        <div className='bg-white px-6 py-8 mb-4 shadow-md rounded-md border m-4 md:m-0'>
          <form onSubmit={submitForm}>
            <h2 className='text-3xl text-center font-semibold mb-6'>Add Aircraft</h2>

            <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Aircraft Registration
              </label>
              <input
                type='text'
                id='registration'
                name='registration'
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder=''
                required
                value={registration}
                onChange={(e) => setRegistration(e.target.value)}
              />
            </div>

             <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Aircraft Type
              </label>
              <input
                type='text'
                id='aircrafttype'
                name='aircrafttype'
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder=''
                required
                value={aircrafttype}
                onChange={(e) => setAircraftType(e.target.value)}
              />
            </div>
          
            <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Seating Capacity
              </label>
              <input
                type='text'
                id='seatingcapacity'
                name='seatingcapacity'
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder='Company Location'
                required
                value={seatingcapacity}
                onChange={(e) => setLocation(e.target.value)}
              />
            </div>
          </form>
        </div>
      </div>
    </section>
  );
};
export default AddAircraftPage;
