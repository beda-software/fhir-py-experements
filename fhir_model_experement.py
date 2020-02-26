import asyncio
from fhirpy import AsyncFHIRClient
from fhirpy.lib import AsyncFHIRResource
from model.fhirelementfactory import FHIRElementFactory
from model.patient import Patient


async def update(self, server=None):
    if server is not None:
        raise Exception("Can't ovveride server")

    data = self.as_json()
    r = AsyncFHIRResource(self.client, self.resource_type, **data)
    await r.save()
    self.update_with_json(r.serialize())
    return self


def fhir_model_adapter(self, **kwargs):
    resource_type = kwargs.pop("resource_type")
    instance = FHIRElementFactory.instantiate(resource_type, kwargs)
    instance.client = self
    instance.update = lambda: update(instance)
    instance.create = lambda: update(instance)
    return instance


async def main():
    client = AsyncFHIRClient("http://test.fhir.org/r4", authorization="Bearer TOKEN",)
    client.resource_class = fhir_model_adapter

    p: Patient = client.resource("Patient")
    print(p)
    await p.create()
    print(p.name)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
