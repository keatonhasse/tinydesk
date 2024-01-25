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
  const [audio, setAudio] = useState<string | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/episodes')
      .then(async (res) => {
        setEpisodes(await res.json());
      });
  }, [setEpisodes]);

  function formatDate(timestamp: number): string {
    const date = new Date(timestamp * 1000);
    return date.toLocaleString('en-US', {
      month: 'long',
      day: '2-digit',
      year: 'numeric'
    });
  };

  const Thumbnail = (props: { url: string }) => (
    props.url ? <img loading="lazy" src={`${props.url}?s=200`} />
      : <div className="placeholder-thumbnail">no thumbnail</div>
  );

  const EpisodeListItem = (props: { episode: Episode }) => (
    <li className='episode-container'>
      <Thumbnail url={props.episode.thumbnail} />
      <div>
        <a href={props.episode.url}><h2>{props.episode.title}</h2></a>
        <div>{formatDate(props.episode.timestamp)}</div>
      </div>
      <div className='media' onClick={() => setAudio(props.episode.id)}></div>
    </li>
  );

  const EpisodeList = () => (
    <ol className='episode-list'>
      {episodes.map((episode) => <EpisodeListItem key={episode.id} episode={episode} />)}
    </ol>
  );

  function PlayPauseButton() {
    const [playing, setPlaying] = useState(false);

    const Play = () => {
      return (
        <svg viewBox="0 0 60 60">
          <polygon points="0,0 50,30 0,60" />
        </svg>
      );
    };

    const Pause = () => {
      return (
        <svg viewBox="0 0 60 60">
          <polygon points="0,0 15,0 15,60 0,60" />
          <polygon points="25,0 40,0 40,60 25,60" />
        </svg>
      );
    };

    const handleClick = () => {
      setPlaying(!playing);
    };

    return (
      <div onClick={handleClick} className='play-pause'>
        {playing ? <Pause /> : <Play />}
      </div>
    );
  }

  const Footer = () => (
    <div className='footer'>
      {audio && <audio src={`http://localhost:8000/episodes/${audio}`}></audio>}
      <PlayPauseButton />
      <div className='media-s'>
        <div className='media-info'>
          <div>title</div>
          <div>artist</div>
        </div>
        <input type="range" />
      </div>
      <input type="range" />
    </div>
  );

  return (
    <>
      <input type="text" className='search' />
      <EpisodeList />
      <Footer />
    </>
  );
}

export default App;
