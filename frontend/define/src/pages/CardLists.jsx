import React from 'react'

const CardLists = () => {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCards = async () => {
      const apiUrl = ForAircraft ? 'http://127.0.0.1:8000/api/get-aircraft/' : 'http://127.0.0.1:8000/api/put-aircraft/';
      try {
        const res = await fetch(apiUrl);
        const data = await res.json();
        setCards(data);
      } catch (error) {
        console.log('Error fetching data', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCards();
  }, []);
    

  return (
    <section className='bg-blue-50 px-4 py-10'>
      <div className='container-xl lg:container m-auto'>
        <h2 className='text-3xl font-bold text-indigo-500 mb-6 text-center'>
          {ForAircraft? 'Aircraft List' : 'Flight List'}
        </h2>

        {loading ? (
          <Spinner loading={loading} />
        ) : (
          <div className='grid grid-cols-1 md:grid-cols-3 gap-6'>
            {cards.map((card) => (
              <Card key={card.aircraft_registraion} card={card} />
            ))}
          </div>
        )}
      </div>
    </section>
  );
};
export default CardList