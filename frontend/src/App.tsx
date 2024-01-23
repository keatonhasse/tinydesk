import { useState, useEffect } from 'react';
import './App.css';

interface Episode {
  id: string,
  url: string,
  title: string,
  timestamp: number,
  thumbnail: string
}

function App() {
  const [episodes, setEpisodes] = useState<Episode[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/episodes')
      .then(async (res) => {
        setEpisodes(await res.json());
      })
      .catch((error) => { console.log(error) })
  }, [setEpisodes]);

  function formatDate(episode: Episode): string {
    const date = new Date(episode.timestamp * 1000);
    return date.toLocaleString('en-US', {
      // 12 hour > 24 hour
      hour12: false,
      month: 'long',
      day: '2-digit',
      year: 'numeric'
    });
  }

  function thumbnail(url: string) {
    if (!url) {
      return <div className='placeholder-thumbnail'>no thumbnail</div>
    }
    return <img loading="lazy" src={`${url}?s=200`} className='thumbnail' />
  }

  return (
    <ol className='container'>
      {episodes.map((episode) => {
        return (
          <li key={episode.id} className='episode-container'>
            {thumbnail(episode.thumbnail)}
            <div>
              <a href={episode.url}><h2>{episode.title}</h2></a>
              <div>{formatDate(episode)}</div>
            </div>
            <div className='media'></div>
          </li>
        );
      })}
    </ol>
  );
}

export default App;
