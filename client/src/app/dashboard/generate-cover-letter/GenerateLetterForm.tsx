import { PhotoIcon, UserCircleIcon } from '@heroicons/react/24/solid'
import { ChevronDownIcon } from '@heroicons/react/16/solid'

export default function GenerateLetterForm() {
  return (
    <div className="max-w-[700px] mx-auto">
      <div className="grid gap-x-8 gap-y-8 ">
        

        <form className="bg-white shadow-xl ring-1 ring-gray-900/5 rounded-xl ">
          <div className=" border-b border-gray-900/10 px-4 sm:py-6 pt-5 pb-1 sm:px-6 sm:flex sm:items-center sm:justify-between">
              <h3 className="text-lg sm:text-md text-base font-semibold text-gray-900">Generate Cover Letter</h3>
              <div className="mt-3 flex sm:mt-0 sm:ml-4">
                  {/* <button
                  type="button"
                  className="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs ring-1 ring-gray-300 ring-inset hover:bg-gray-50"
                  >
                  Share
                  </button> */}
                  {/* <button
                  type="button"
                  className="cursor-pointer ml-3 inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                  >
                  Edit
                  </button> */}
              </div>
          </div>
          
          <div className="px-4 py-6 sm:p-8">
            <div className="grid gap-10 max-w-2xl">
              

              {/* Company Name and Job Title */}
              <div className='flex gap-x-6 gap-y-6 sm:gap-y-0 sm:flex-row flex-col'>

                {/* Company Name */}
                <div className="sm:w-1/2 w-full">
                  <label htmlFor="username" className="block text-[15px] font-medium text-gray-900">
                    Company Name
                  </label>
                  <div className="mt-2">
                    <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
                      <div className="shrink-0 text-base text-gray-500 select-none sm:text-sm/6"></div>
                      <input
                        id="username"
                        name="username"
                        type="text"
                        placeholder="Enter Name"
                        className="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
                      />
                    </div>
                  </div>
                </div>
                
                {/* Job Title */}
                <div className="sm:w-1/2 w-full">
                  <label htmlFor="username" className="block text-[15px] font-medium text-gray-900">
                      Job Title
                  </label>
                  <div className="mt-2">
                    <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
                      <div className="shrink-0 text-base text-gray-500 select-none sm:text-sm/6"></div>
                      <input
                        id="username"
                        name="username"
                        type="text"
                        placeholder="Enter Title"
                        className="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
                      />
                    </div>
                  </div>
                </div>
              </div>

              

              {/* Job Posting */}
              <div className="">
                <label htmlFor="comment" className="block text-[15px] font-medium text-gray-900">
                  Job Description
                </label>
                <div className="mt-2">
                  <textarea
                    id="comment"
                    name="comment"
                    rows={4}
                    placeholder="Paste the job posting here. "
                    className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                    defaultValue={''}
                  />
                </div>
              </div>
           

              
            </div>
          </div>
          <div className="flex items-center justify-end gap-x-6 border-t border-gray-900/10 px-4 py-4 sm:px-8">
            
            <button
              type="submit"
              className="cursor-pointer flex gap-2 items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Generate Cover Letter
              <img src="/logo-white.png" alt="plus" className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>
    </div>









  )
}
