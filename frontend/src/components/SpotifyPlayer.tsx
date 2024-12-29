import { useEffect, useState } from 'react'

const SpotifyPlayer = () => {
  // Explicitly typed state
  const [player, setPlayer] = useState<Spotify.Player | null>(null)
  const [currentTrack, setCurrentTrack] = useState<string>("No track playing")

  useEffect(() => {
    // This function is called when Spotify SDK is ready
    window.onSpotifyWebPlaybackSDKReady = () => {
      // Create a new player instance
      const newPlayer = new window.Spotify.Player({
        name: 'Light Symphony',
        getOAuthToken: callback => { 
          // Spotify will call this function when it needs a token
          // We'll implement proper token handling soon
          callback('YOUR_ACCESS_TOKEN')
        }
      })

      // Listen for when the player is ready
      newPlayer.addListener('ready', ({ device_id }: { device_id: string }) => {
        console.log('Ready with Device ID', device_id)
      })

      // Listen for when the player becomes not ready
      newPlayer.addListener('not_ready', ({ device_id }: { device_id: string }) => {
        console.log('Device ID has gone offline', device_id)
      })

      // Listen for track changes
      newPlayer.addListener('player_state_changed', state => {
        if (state && state.track_window.current_track) {
          setCurrentTrack(state.track_window.current_track.name)
        }
      })

      // Connect to the player
      newPlayer.connect()
      setPlayer(newPlayer)
    }
  }, [])  // Empty dependency array means this effect runs once on mount

  return (
    <div>
      <h2>Spotify Player Status</h2>
      <p>{currentTrack}</p>
    </div>
  )
}

export default SpotifyPlayer