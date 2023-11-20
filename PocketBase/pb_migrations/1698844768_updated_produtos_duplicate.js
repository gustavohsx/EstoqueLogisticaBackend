/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("vfdp7ew4fyzz9tu")

  collection.name = "produtos"

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("vfdp7ew4fyzz9tu")

  collection.name = "produtos_duplicate"

  return dao.saveCollection(collection)
})
