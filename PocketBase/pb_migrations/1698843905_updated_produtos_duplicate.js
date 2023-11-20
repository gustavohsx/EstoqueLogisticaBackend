/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8w0s6oruyjof7eg")

  collection.name = "produtos"

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8w0s6oruyjof7eg")

  collection.name = "produtos_duplicate"

  return dao.saveCollection(collection)
})
