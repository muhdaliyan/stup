"""arrange mean — MongoDB + Express + Angular + Node scaffold."""

from arrange.utils import (
    check_node,
    check_tool,
    create_dirs,
    print_banner,
    print_done,
    print_step,
    run,
    write_file,
)

# ── Server templates ─────────────────────────────────────────────────

SERVER_INDEX = '''\
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use("/api", require("./routes/api"));

// Health check
app.get("/health", (req, res) => res.json({ status: "ok" }));

// Connect to MongoDB & start server
mongoose
  .connect(process.env.MONGO_URI)
  .then(() => {
    console.log("✓ Connected to MongoDB");
    app.listen(PORT, () => console.log(`✓ Server running on port ${PORT}`));
  })
  .catch((err) => console.error("✗ MongoDB connection error:", err));
'''

SERVER_ROUTES_API = '''\
const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
  res.json({ message: "API is working!" });
});

module.exports = router;
'''

SERVER_MODELS_EXAMPLE = '''\
const mongoose = require("mongoose");

const ExampleSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },
    description: { type: String, default: "" },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Example", ExampleSchema);
'''

PROXY_CONF = '''\
{
  "/api": {
    "target": "http://localhost:5000",
    "secure": false,
    "changeOrigin": true
  }
}
'''

ENV_FILE = '''\
PORT=5000
MONGO_URI=mongodb://localhost:27017/myapp
NODE_ENV=development
'''

ROOT_PACKAGE_JSON = '''\
{
  "name": "mean-app",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "server": "cd server && node index.js",
    "client": "cd client && npx ng serve --proxy-config proxy.conf.json",
    "dev": "npx concurrently \\"npm run server\\" \\"npm run client\\""
  },
  "devDependencies": {
    "concurrently": "^8.0.0"
  }
}
'''


def run_command() -> None:
    """Scaffold a MEAN stack project."""
    print_banner("mean", "MongoDB + Express + Angular + Node")

    check_node()

    # ── Server ───────────────────────────────────────────────────────
    create_dirs("server/routes", "server/models", "server/config")

    run("npm init -y", cwd="server")
    run("npm install express mongoose dotenv cors", cwd="server")

    write_file("server/index.js", SERVER_INDEX)
    write_file("server/routes/api.js", SERVER_ROUTES_API)
    write_file("server/models/Example.js", SERVER_MODELS_EXAMPLE)

    # ── Angular client ───────────────────────────────────────────────
    print_step("Creating Angular app (this may take a moment)...")
    run("npx -y @angular/cli@latest new client --defaults --skip-git --style=css --routing")

    write_file("proxy.conf.json", PROXY_CONF)

    # ── Root config ──────────────────────────────────────────────────
    write_file("package.json", ROOT_PACKAGE_JSON)
    run("npm install")
    write_file(".env", ENV_FILE)

    print_done()
