#[macro_use]
extern crate rustless;
extern crate hyper;
extern crate iron;
extern crate rustc_serialize as serialize;
extern crate valico;

use valico::json_dsl;
use hyper::status::StatusCode;
use rustless::{
    Application, Api, Nesting, Versioning
};
use rustless::json::ToJson;

fn main() {

    let api = Api::build(|api| {
        // Specify API version
        api.version("v1", Versioning::AcceptHeader("chat"));
        api.prefix("api");

        // Create API for chats
        api.mount(Api::build(|chats_api| {

            chats_api.after(|client, _params| {
                client.set_status(StatusCode::NotFound);
                Ok(())
            });

            // Add namespace
            chats_api.namespace("chats/:id", |chat_ns| {

                // Valico settings for this namespace
                chat_ns.params(|params| {
                    params.req_typed("id", json_dsl::u64())
                });

                // Create endpoint for POST /chats/:id/users/:user_id
                chat_ns.post("users/:user_id", |endpoint| {

                    // Add description
                    endpoint.desc("Update user");

                    // Valico settings for endpoint params
                    endpoint.params(|params| {
                        params.req_typed("user_id", json_dsl::u64());
                        params.req_typed("id", json_dsl::string())
                    });

                    endpoint.handle(|client, params| {
                        client.json(&params.to_json())
                    })
                });

            });
        }));
    });

    let app = Application::new(api);

    iron::Iron::new(app).http("0.0.0.0:4000").unwrap();
    println!("On 4000");

    println!("Rustless server started!");
}
