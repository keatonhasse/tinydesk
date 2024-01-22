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
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch('http://localhost:8000/episodes')
      .then(async (res) => {
        setEpisodes(await res.json());
        setIsLoading(false);
      })
      .catch((error) => { console.log(error) })
  }, [setEpisodes, isLoading]);

  function getThumbnail(episode: Episode): string {
    const date = new Date(episode.timestamp * 1000);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const tsDate = `${year}/${month}/${day}`;
    return `https://media.npr.org/assets/img/${tsDate}/${episode.thumbnail}?s=200`;
  }

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

  return (
    <div>
      {episodes.map((episode) => {
        return (
          <div key={episode.id}>
            <img src={getThumbnail(episode)} />
            <p>{episode.title}</p>
            <p>{formatDate(episode)}</p>
          </div>
        );
      })}
    </div>
  );
}

export default App;
