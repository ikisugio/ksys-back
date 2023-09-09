const express = require("express");
const { config, normalize } = require("@geolonia/normalize-japanese-addresses");
const app = express();
const PORT = 3001; // 任意のポート番号

// normalize.jsが存在するディレクトリのjapanese-addresses-masterを指定
config.japaneseAddressesApi =
  "file://" + __dirname + "/japanese-addresses-master/api/ja";

app.use(express.json());

app.post("/normalize", async (req, res) => {
  const address = req.body.address;
  const result = await normalize(address);
  res.json(result);
});

app.listen(PORT, () => {
  console.log(`Node server is running on port ${PORT}`);
});
