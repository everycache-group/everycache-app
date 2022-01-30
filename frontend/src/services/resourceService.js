import * as api from "../api/api-core";

export default class ResourceConnector {
  constructor(resource) {
    this.resource = resource;
  }

  create = async (data) => await api.create(this.resource, data);

  remove = async (id) => await api.remove(this.resource, id);

  update = async (id, data) => await api.update(this.resource, id, data);

  get = async (id) => await api.get(this.resource, id);
}
