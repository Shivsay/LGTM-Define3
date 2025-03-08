import { Outlet } from 'react-router-dom';
// import NavBar from '../components/NavBar';
// import { NavigationMenu, NavigationMenuItem, NavigationMenuList } from "@/components/ui/navigation-menu";
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from 'react-router-dom';

const MainLayout = () => {
  return (
    <>
      <NavBar />  
      <Outlet />
      <Footer />
    </>
  );
};
export default MainLayout;
