const people = [
    { name: 'Company 1', title: 'Front-end Developer', date: '07/28/2025', key: '1' },
    { name: 'Company 2', title: 'Front-end Developer', date: '07/28/2025', key: '2' },
    { name: 'Company 3', title: 'Front-end Developer', date: '07/28/2025', key: '3' },
    // More people...
  ]
  
  export default function Example() {
    return (
      <div className="px-6 py-8 bg-white rounded-lg shadow-md overflow-y-auto">
        <div className="sm:flex sm:items-center">
          <div className="sm:flex-auto">
            <h1 className="text-base font-semibold text-gray-900">Previous Cover Letters</h1>
            {/* <p className="mt-2 text-sm text-gray-700">
              A list of all the users in your account including their name, title, email and role.
            </p> */}
          </div>
          <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
            <button
              type="button"
              className="cursor-pointer flex gap-2 items-center block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Generate Cover Letter
              <img src="/logo-white.png" alt="plus" className="w-5 h-5" />
            </button>
          </div>
        </div>
        <div className="mt-8 flow-root">
          <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
              <table className="min-w-full divide-y divide-gray-300">
                <thead>
                  <tr>
                    <th scope="col" className="py-3.5 pr-3 pl-4 text-left text-sm font-semibold text-gray-900 sm:pl-0">
                      Company
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Job Title
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Date
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Actions
                    </th>
                    
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {people.map((person) => (
                    <tr key={person.key}>
                      <td className="py-4 pr-3 pl-4 text-sm font-medium whitespace-nowrap text-gray-900 sm:pl-0">
                        {person.name}
                      </td>
                      <td className="px-3 py-4 text-sm whitespace-nowrap text-gray-500">{person.title}</td>
                      <td className="px-3 py-4 text-sm whitespace-nowrap text-gray-500">{person.date}</td>
                      <td className="px-3 py-4 text-sm whitespace-nowrap text-gray-500">
                        <button className="cursor-pointer text-indigo-600 hover:text-indigo-900">
                          View
                        </button>
                      </td>
                      {/* <td className="relative py-4 pr-4 pl-3 text-right text-sm font-medium whitespace-nowrap sm:pr-0">
                        <a href="#" className="text-indigo-600 hover:text-indigo-900">
                          Edit<span className="sr-only">, {person.name}</span>
                        </a>
                      </td> */}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    )
  }
  