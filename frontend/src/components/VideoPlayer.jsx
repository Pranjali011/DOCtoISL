export default function VideoPlayer({ videoUrl }) {
  console.log("VIDEO URL RECEIVED:", videoUrl);

  if (!videoUrl) return null;

  return (
    <div className="video-card">
      <h3 className="video-title">ISL Video</h3>

      <video
        controls
        className="video-player"
        onError={(e) => console.error("VIDEO ERROR:", e)}
      >
        <source src={videoUrl} type="video/mp4" />
      </video>
    </div>
  );
}
