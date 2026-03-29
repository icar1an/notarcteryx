export default {
  async scheduled(event, env, ctx) {
    const res = await fetch("https://notarcteryx-api.onrender.com/health");
    const data = await res.json();
    console.log(`Ping: ${data.status}, mountains: ${data.mountains_loaded}`);
  },
};
